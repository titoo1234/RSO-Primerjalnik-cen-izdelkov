CREATE TABLE Trgovine (
    Id  INT PRIMARY KEY IDENTITY,
    Ime VARCHAR(100)    NOT NULL
                UNIQUE
);


CREATE TABLE Kategorije (
    Id  INT PRIMARY KEY IDENTITY,
    Ime VARCHAR(100)    NOT NULL
                UNIQUE
);

CREATE TABLE Podkategorije (
    Id         INT PRIMARY KEY IDENTITY,
    Ime        VARCHAR(100)    NOT NULL,
    Kategorija INT REFERENCES Kategorije (Id),
    UNIQUE (
        Ime,
        Kategorija
    )
);

CREATE TABLE Izdelki (
    Id            INT PRIMARY KEY IDENTITY,
    Ime           VARCHAR(100)    NOT NULL,
    Kategorija    INT REFERENCES Kategorije (Id),
    Podkategorija INT REFERENCES Podkategorije (Id),
    Trgovina      INT REFERENCES Trgovine (Id),
    Cena          DECIMAL NOT NULL,
    UNIQUE (
        Ime,
        Trgovina,
        Cena
    )
);

CREATE TABLE Uporabniki (
    Id    INT  PRIMARY KEY IDENTITY,
    Ime   VARCHAR(100)     UNIQUE
                   NOT NULL,
    Geslo VARCHAR(100) NOT NULL,
    Admin INT
);

CREATE TABLE Kosarica (
    Uporabnik INT REFERENCES Uporabniki (Id),
    Izdelek   INT REFERENCES Izdelki (Id) 
                      UNIQUE,
    Kolicina  DECIMAL,
    Cena      DECIMAL,
    Trgovina  INTEGER REFERENCES Trgovine (Id) 
);



INSERT INTO Trgovine (Ime) VALUES ('Mercator')
INSERT INTO Trgovine (Ime) VALUES ('Tus')


INSERT INTO Kategorije (Ime) VALUES ('Meso')

INSERT INTO Podkategorije (Ime,Kategorija) VALUES ('Svinjsko meso',1)

INSERT INTO Izdelki (Ime,Kategorija,Podkategorija,Trgovina,Cena) VALUES ('Ribica',1,1,1,13.79)



INSERT INTO Uporabniki (Ime,Geslo,Admin) VALUES ('Janez123','asdhuvqoasdjv',0)

INSERT INTO Kosarica (Uporabnik, Izdelek, Kolicina, Cena, Trgovina) VALUES (1,1,1,13.79,1)