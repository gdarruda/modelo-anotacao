CREATE TABLE anotacoes
(
  id_anotacao INTEGER AUTO_INCREMENT,
  nome        TEXT,
  PRIMARY KEY (id_anotacao)
);

CREATE TABLE noticias_x_anotacao
(
 id_noticia  INTEGER,
 id_anotacao INTEGER,
 completo    FLOAT,
 PRIMARY KEY (id_anotacao, id_noticia)
);

ALTER TABLE noticias_x_anotacao ADD CONSTRAINT fk_noticias_anotacao FOREIGN KEY (id_noticia) REFERENCES noticias(id_noticia);
ALTER TABLE noticias_x_anotacao ADD CONSTRAINT fk_anotacao_noticia FOREIGN KEY (id_anotacao) REFERENCES anotacoes(id_anotacao);

CREATE TABLE noticias_x_paragrafo
(
 id_paragrafo  INTEGER,
 id_noticia    INTEGER,
 id_anotacao   INTEGER,
 paragrafo     TEXT,
 ini_posic     INTEGER,
 fim_posic     INTEGER,
 polaridade    VARCHAR(2),
 entidade      TEXT,
 PRIMARY KEY (id_paragrafo, id_noticia, id_anotacao)
);

ALTER TABLE noticias_x_paragrafo ADD CONSTRAINT fk_paragrafos_x_noticias FOREIGN KEY (id_noticia, id_anotacao) REFERENCES noticias_x_anotacao(id_noticia, id_anotacao);
