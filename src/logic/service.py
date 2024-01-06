import time
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

from typing import List

from project_shkedia_models import search, media, insights, jobs
from db.service import MediaDBService

class MonthsEngineLogics:

    def __init__(self,
                 media_db_service: MediaDBService,
                 engine_details: insights.InsightEngine,
                 batch_process_size: int = 200,
                 batch_processing_period_minutes: float = 120,) -> None:
        self.media_db_service = media_db_service
        self.batch_process_size = batch_process_size
        self.batch_processing_period_minutes = batch_processing_period_minutes
        self.engine = self.__init_engine__(engine_details)


    def __init_engine__(self,local_engine_details):
        search_results = self.media_db_service.search_engine(engine_name=local_engine_details.name)
        if search_results.total_results_number > 0:
            return insights.InsightEngine(**search_results.results[0])
        #TODO: Create the engine in the db if not exists           
        #TODO: Updates the engine details if needed


    def create_jobs(self):
        media_to_process: search.SearchResult = self.media_db_service.get_media_to_analyze(engine_name=self.engine.name, batch_size=self.batch_process_size)
        job_list: List[jobs.InsightJob] = []
        for result in media_to_process.results:
            media_item = media.MediaStorage(**result)
            temp_job = jobs.InsightJob(insight_engine_id=self.engine.id,
                                        media_id=media_item.media_id)
            logger.info(f"Create new job ({temp_job.id}) for media ({media_item.media_id})")
            job_list.append(temp_job)
        if len(job_list)>0:
            self.media_db_service.put_jobs(job_list)

    def __extract_insights_logics__(self, job_id, media_item) -> List[insights.Insight]:
        insights_list = []
        # TODO: Implement the insight extraction here.
        
        calculated_insight = ...
        logger.info(f"Process job ({job_id}). Added insight calculated: {media_item.name}")
        insights_list.append(insights.Insight(insight_engine_id=self.engine.id,
                                                      media_id=media_item.media_id,
                                                      name=calculated_insight,
                                                      job_id=job_id,
                                                      status=insights.InsightStatusEnum.APPROVED))
        return insights_list

    def listen(self):
        while True:
            try:
                self.create_jobs()
            except Exception as err:
                logger.warning(f"Failed to create jobs: {str(err)}")
            logger.info("Search jobs")
            jobs_to_process: search.SearchResult = self.media_db_service.get_pending_jobs(engine_id=self.engine.id, batch_size=self.batch_process_size)
            jobs_to_process: List[jobs.InsightJob] = [jobs.InsightJob(**item) for item in jobs_to_process.results]
            media_to_process: search.SearchResult = self.media_db_service.get_media_by_ids(media_ids_list=[item.media_id for item in jobs_to_process])
            media_to_process: List[media.MediaIDs] = [media.MediaIDs(**media_item) for media_item in media_to_process.results]
            analyzing_dictionary = {}
            for job in jobs_to_process:
                analyzing_dictionary[job.id] = (job,[media_item for media_item in media_to_process if media_item.media_id==job.media_id][0])
            
            insights_list = []
            for job_id,value in analyzing_dictionary.items():
                temp_job,media_item = value
                insights_list += self.__extract_insights_logics__(temp_job.id,media_item)
            if len(insights_list)>0:
                self.media_db_service.put_insights(insights_list)
            if len(jobs_to_process)>0:
                for job in jobs_to_process:
                    job.status = jobs.InsightJobStatus.DONE
                    job.end_time = datetime.now()
                if not self.media_db_service.update_jobs(jobs_to_process)>0:
                    logger.error(f"Could not update job {jobs_to_process}")
            if len(jobs_to_process)==0:
                time.sleep(self.batch_processing_period_minutes*60)


