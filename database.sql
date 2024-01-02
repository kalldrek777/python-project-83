DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL
);
CREATE TABLE url_checks (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT REFERENCES urlS(id) NOT NULL,
    status_code INT,
    h1 TEXT,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP NOT NULL
);