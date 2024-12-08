DROP DATABASE IF EXISTS SUR;
CREATE DATABASE SUR;
USE SUR;

CREATE TABLE Genre (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Artist (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    bio VARCHAR(255),
    country VARCHAR(50) NOT NULL
);

CREATE TABLE Album (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    genre_id INT,
    artist_id INT NOT NULL,
    album_type ENUM('Single', 'EP', 'Mini Album', 'Full Album'),
    release_date DATE,
    FOREIGN KEY (genre_id) REFERENCES Genre(genre_id),
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
);

CREATE TABLE Song (
    song_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    duration TIME NOT NULL,
    release_date DATE,
    album_id INT,
    genre_id INT NOT NULL,
    artist_id INT NOT NULL,
    playbacks INT DEFAULT 0,
    FOREIGN KEY (album_id) REFERENCES Album(album_id),
    FOREIGN KEY (genre_id) REFERENCES Genre(genre_id),
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
);

CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    age INT,
    country VARCHAR(50) NOT NULL
);

CREATE TABLE Playlist (
    playlist_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    user_id INT NOT NULL,
    create_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Following (
    user_id INT NOT NULL,
    artist_id INT NOT NULL,
    PRIMARY KEY (user_id, artist_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
);

CREATE TABLE Playlist_Song (
    playlist_id INT NOT NULL,
    song_id INT NOT NULL,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id),
    FOREIGN KEY (song_id) REFERENCES Song(song_id)
);

DELIMITER //

-- Trigger for BEFORE INSERT
CREATE TRIGGER calculate_user_age_before_insert
BEFORE INSERT ON User
FOR EACH ROW
BEGIN
    IF NEW.date_of_birth IS NOT NULL THEN
        -- Calculate age based on the current date and the date_of_birth
        SET NEW.age = TIMESTAMPDIFF(YEAR, NEW.date_of_birth, CURDATE());

        -- Adjust the age if the birthday hasn't occurred this year
        IF DATE_ADD(NEW.date_of_birth, INTERVAL TIMESTAMPDIFF(YEAR, NEW.date_of_birth, CURDATE()) YEAR) > CURDATE() THEN
            SET NEW.age = NEW.age - 1;
        END IF;
    ELSE
        -- If date_of_birth is NULL, set age to NULL
        SET NEW.age = NULL;
    END IF;
END;
//

-- Trigger for BEFORE UPDATE
CREATE TRIGGER calculate_user_age_before_update
BEFORE UPDATE ON User
FOR EACH ROW
BEGIN
    IF NEW.date_of_birth IS NOT NULL THEN
        -- Calculate age based on the current date and the date_of_birth
        SET NEW.age = TIMESTAMPDIFF(YEAR, NEW.date_of_birth, CURDATE());

        -- Adjust the age if the birthday hasn't occurred this year
        IF DATE_ADD(NEW.date_of_birth, INTERVAL TIMESTAMPDIFF(YEAR, NEW.date_of_birth, CURDATE()) YEAR) > CURDATE() THEN
            SET NEW.age = NEW.age - 1;
        END IF;
    ELSE
        -- If date_of_birth is NULL, set age to NULL
        SET NEW.age = NULL;
    END IF;
END;
//


-- Trigger to update `update_date` for playlist whenever a song is added or removed
CREATE TRIGGER update_playlist_update_date
AFTER INSERT ON Playlist_Song
FOR EACH ROW
BEGIN
    -- When a song is added to a playlist, update the `update_date`
    UPDATE Playlist
    SET update_date = CURRENT_TIMESTAMP
    WHERE playlist_id = NEW.playlist_id;
END; //

CREATE TRIGGER update_playlist_update_date2
AFTER DELETE ON Playlist_Song
FOR EACH ROW
BEGIN
    -- When a song is removed to a playlist, update the `update_date`
    UPDATE Playlist
    SET update_date = CURRENT_TIMESTAMP
    WHERE playlist_id = OLD.playlist_id;
END; //


-- Trigger to prevent artist deletion if they have albums or songs
CREATE TRIGGER prevent_artist_deletion
BEFORE DELETE ON Artist
FOR EACH ROW
BEGIN
    DECLARE album_count INT;
    DECLARE song_count INT;

    -- Check if artist is associated with any albums or songs
    SELECT COUNT(*) INTO album_count FROM Album WHERE artist_id = OLD.artist_id;
    SELECT COUNT(*) INTO song_count FROM Song WHERE artist_id = OLD.artist_id;

    IF album_count > 0 OR song_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete artist, they have associated albums or songs';
    END IF;
END; //

-- Trigger to ensure user email uniqueness when updating user details
CREATE TRIGGER check_unique_user_email
BEFORE UPDATE ON User
FOR EACH ROW
BEGIN
    -- Ensure no other user has the same email when updating
    IF EXISTS (SELECT 1 FROM User WHERE email = NEW.email AND user_id != OLD.user_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Email must be unique';
    END IF;
END; //

-- Trigger to ensure user email uniqueness when inserting user details
CREATE TRIGGER check_unique_user_email2
BEFORE INSERT ON User
FOR EACH ROW
BEGIN
    -- Ensure no other user has the same email when inserting
    IF EXISTS (SELECT 1 FROM User WHERE email = NEW.email) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Email must be unique';
    END IF;
END; //

-- Stored procedure to create a user
CREATE PROCEDURE create_user(
    IN firstName VARCHAR(50),
    IN lastName VARCHAR(50),
    IN email VARCHAR(100),
    IN passwordHash VARCHAR(255),
    IN dateOfBirth DATE,
    IN country VARCHAR(50)
)
BEGIN
    INSERT INTO User (first_name, last_name, email, password_hash, date_of_birth, country)
    VALUES (firstName, lastName, email, passwordHash, dateOfBirth, country);
END; //

-- Procedure to update the user's first name
CREATE PROCEDURE update_user_first_name(
    IN userId INT,
    IN firstName VARCHAR(50)
)
BEGIN
    UPDATE User
    SET first_name = firstName
    WHERE user_id = userId;
END; //

-- Procedure to update the user's last name
CREATE PROCEDURE update_user_last_name(
    IN userId INT,
    IN lastName VARCHAR(50)
)
BEGIN
    UPDATE User
    SET last_name = lastName
    WHERE user_id = userId;
END; //

-- Procedure to update the user's email
CREATE PROCEDURE update_user_email(
    IN userId INT,
    IN email VARCHAR(100)
)
BEGIN
    UPDATE User
    SET email = email
    WHERE user_id = userId;
END; //

-- Procedure to update the user's password hash
CREATE PROCEDURE update_user_password_hash(
    IN userId INT,
    IN passwordHash VARCHAR(255)
)
BEGIN
    UPDATE User
    SET password_hash = passwordHash
    WHERE user_id = userId;
END; //

-- Procedure to update the user's date of birth
CREATE PROCEDURE update_user_date_of_birth(
    IN userId INT,
    IN dateOfBirth DATE
)
BEGIN
    UPDATE User
    SET date_of_birth = dateOfBirth
    WHERE user_id = userId;
END; //

-- Procedure to update the user's country
CREATE PROCEDURE update_user_country(
    IN userId INT,
    IN country VARCHAR(50)
)
BEGIN
    UPDATE User
    SET country = country
    WHERE user_id = userId;
END; //


-- Stored procedure to create an artist
CREATE PROCEDURE create_artist(
    IN firstName VARCHAR(50),
    IN lastName VARCHAR(50),
    IN email VARCHAR(100),
    IN passwordHash VARCHAR(255),
    IN dateOfBirth DATE,
    IN bio TEXT,
    IN country VARCHAR(50)
)
BEGIN
    INSERT INTO Artist (first_name, last_name, email, password_hash, date_of_birth, bio, country)
    VALUES (firstName, lastName, email, passwordHash, dateOfBirth, bio, country);
END; //

-- Procedure to update the artist's first name
CREATE PROCEDURE update_artist_first_name(
    IN artistId INT,
    IN firstName VARCHAR(50)
)
BEGIN
    UPDATE Artist
    SET first_name = firstName
    WHERE artist_id = artistId;
END; //

-- Procedure to update the artist's last name
CREATE PROCEDURE update_artist_last_name(
    IN artistId INT,
    IN lastName VARCHAR(50)
)
BEGIN
    UPDATE Artist
    SET last_name = lastName
    WHERE artist_id = artistId;
END; //

-- Procedure to update the artist's email
CREATE PROCEDURE update_artist_email(
    IN artistId INT,
    IN email VARCHAR(100)
)
BEGIN
    UPDATE Artist
    SET email = email
    WHERE artist_id = artistId;
END; //

-- Procedure to update the artist's password hash
CREATE PROCEDURE update_artist_password_hash(
    IN artistId INT,
    IN passwordHash VARCHAR(255)
)
BEGIN
    UPDATE Artist
    SET password_hash = passwordHash
    WHERE artist_id = artistId;
END; //

-- Procedure to update the artist's date of birth
CREATE PROCEDURE update_artist_date_of_birth(
    IN artistId INT,
    IN dateOfBirth DATE
)
BEGIN
    UPDATE Artist
    SET date_of_birth = dateOfBirth
    WHERE artist_id = artistId;
END; //

-- Procedure to update the artist's biography
CREATE PROCEDURE update_artist_bio(
    IN artistId INT,
    IN bio TEXT
)
BEGIN
    UPDATE Artist
    SET bio = bio
    WHERE artist_id = artistId;
END; //

-- Procedure to update the artist's country
CREATE PROCEDURE update_artist_country(
    IN artistId INT,
    IN country VARCHAR(50)
)
BEGIN
    UPDATE Artist
    SET country = country
    WHERE artist_id = artistId;
END; //

-- Stored procedure to create a playlist with songs
CREATE PROCEDURE create_playlist_with_songs(
    IN userId INT,
    IN playlistTitle VARCHAR(100),
    IN playlistDescription VARCHAR(255)
)
BEGIN
    DECLARE playlistId INT;
    -- Create the playlist
    INSERT INTO Playlist (title, description, user_id)
    VALUES (playlistTitle, playlistDescription, userId);
END; //

-- Stored procedure to follow/unfollow an artist
CREATE PROCEDURE follow_artist(
    IN userId INT,
    IN artistId INT
)
BEGIN
    -- Check if already following
    IF NOT EXISTS (SELECT 1 FROM Following WHERE user_id = userId AND artist_id = artistId) THEN
        INSERT INTO Following (user_id, artist_id)
        VALUES (userId, artistId);
    ELSE
        -- If already following, unfollow
        DELETE FROM Following WHERE user_id = userId AND artist_id = artistId;
    END IF;
END; //

DELIMITER ;