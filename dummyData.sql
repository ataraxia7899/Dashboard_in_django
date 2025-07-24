CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    join_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 예시 데이터 삽입
INSERT INTO user (username, join_date) VALUES
('Studio_bada', '2024-07-08 09:00:00'),
('윤소영', '2024-07-07 15:00:00'),
('ottosei_yokokawa', '2024-07-06 20:30:00'),
('moca', '2024-07-05 10:20:00'),
('서현', '2024-07-03 14:30:00'),
('존서', '2024-06-15 11:00:00'),
('Zirla', '2024-06-12 08:40:00');


CREATE TABLE post (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    user_id INT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- 예시 데이터 삽입
INSERT INTO post (content, user_id, created_at) VALUES
('pitch cam', 6, '2024-07-08 09:30:00'),
('Plan for next step...', 6, '2024-07-07 13:10:00'),
('O/P 계획 세부 사이트...', 6, '2024-06-26 16:00:00'),
('???가 걸렸다', 7, '2024-06-18 09:15:00'),
('pcn...', 6, '2024-06-16 12:30:00');


CREATE TABLE comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT,
    user_id INT,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES post(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- 예시 데이터 삽입
INSERT INTO comment (post_id, user_id, content, created_at) VALUES
(4, 4, '좋아요!', '2024-06-19 10:22:00'); -- moca가 Zirla 글에 댓글


CREATE TABLE post_like (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT,
    user_id INT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES post(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- 예시 데이터 삽입
INSERT INTO post_like (post_id, user_id, created_at) VALUES
(1, 7, '2024-07-08 10:00:00'), -- Zirla가 존서 글에 좋아요
(2, 7, '2024-07-07 13:30:00');