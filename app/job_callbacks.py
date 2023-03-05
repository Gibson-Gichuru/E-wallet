import os
from config import base_dir, logger_setup


def success(job,connection, results, *args, **kwargs):

    log_file = os.path.join(base_dir, "success_job.log")

    logger = logger_setup("Job-success", log_file)

    logger.info(f"{job.id} success")


def failure(job, connection, type, value, traceback):

    log_file = os.path.join(base_dir, "failure_job.log")

    logger = logger_setup("Job-failure", log_file)

    logger.error(
        "{} failed with {} exception {}".format(
            job.id,
            type,
            value
        )
    )
