
CREATE TABLE IF NOT EXISTS job_runs (
    task_id VARCHAR(128) NOT NULL,
    request_id VARCHAR(80) NOT NULL,
    product_id BIGINT NOT NULL,
    status VARCHAR(32) NOT NULL,
    result_status VARCHAR(32) NULL,
    error_message TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (task_id),
    UNIQUE KEY uq_job_runs_request_id (request_id),
    INDEX idx_job_runs_created (created_at, task_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS listing_results (
    request_id VARCHAR(80) NOT NULL,
    product_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,

    PRIMARY KEY (request_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
