CREATE DATABASE social_news;
\c social_news

CREATE TABLE IF NOT EXISTS stories (
    id INT GENERATED ALWAYS AS IDENTITY,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    created TIMESTAMP NOT NULL,
    modified TIMESTAMP DEFAULT DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp) NOT NULL,
    PRIMARY KEY (id)
);


INSERT INTO stories (title,url,created,modified) VALUES 
('Karen Gillan teams up with Lena Headey and Michelle Yeoh in assassin thriller Gunpowder Milkshake','https://www.empireonline.com/movies/news/gunpowder-milk-shake-lena-headey-karen-gillan-exclusive/','2023-07-04 11:11:18', '2023-07-04 11:11:18'),
('Aukus deal: Summit was projection of power and collaborative intent','https://www.bbc.co.uk/news/uk-politics-64948535','2023-07-04 11:13:14','2023-07-04 11:13:14'),
('SVB and Signature Bank: How bad is US banking crisis and what does it mean?','https://www.bbc.co.uk/news/business-64951630','2023-07-04 11:13:14','2023-07-04 11:13:14'),
('eBird: A crowdsourced bird sighting database','https://ebird.org/home','2023-07-04 11:13:14','2023-07-04 11:13:14'
);

CREATE TABLE IF NOT EXISTS votes (
    vote_id INT GENERATED ALWAYS AS IDENTITY,
    direction TEXT NOT NULL DEFAULT 'up',
    created TIMESTAMP NOT NULL,
    modified TIMESTAMP DEFAULT DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp) NOT NULL,
    id INT,
    PRIMARY KEY (vote_id),
    FOREIGN KEY (id) REFERENCES stories(id) ON DELETE CASCADE
    );

INSERT INTO votes(direction, id, created, modified) VALUES ('up', 1, DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp),DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp));
INSERT INTO votes(direction, id, created, modified) VALUES ('up', 1,DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp),DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp));
INSERT INTO votes(direction, id, created, modified) VALUES ('down', 1, DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp),DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp));
INSERT INTO votes(direction, id, created, modified) VALUES ('down', 3,DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp),DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp));
INSERT INTO votes(direction, id, created, modified) VALUES ('up', 4, DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp),DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp));
INSERT INTO votes(direction, id, created, modified) VALUES ('down', 4, DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp),DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp));
INSERT INTO votes(direction, id, created, modified) VALUES ('down', 4, DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp),DATE_TRUNC('second', CURRENT_TIMESTAMP::timestamp));


