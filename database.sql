CREATE DATABASE proj;
USE proj;



CREATE TABLE tbl_historico_compras(
    id BIGINT IDENTITY(1,1) PRIMARY KEY
);

CREATE TABLE tbl_historico_visualizacoes(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
);


CREATE TABLE tbl_produto(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    nome nvarchar(50) NOT NULL,
    popularidade tinyint CHECK(popularidade BETWEEN 0 AND 100),
    dt_lancamento DATETIME,
    acessos INT CHECK(acessos >= 0),
    compras INT CHECK(compras >= 0),
    preco DECIMAL(10,2) NOT NULL,
    isOferta BIT,
    isLancamento BIT
);

CREATE TABLE tbl_carrinho(
    id BIGINT IDENTITY(1,1) PRIMARY KEY
);

CREATE TABLE tbl_cliente(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    dt_nasc DATETIME NOT NULL,
    genero char(1) NOT NULL,
    cidade varchar(50) NOT NULL,
    estado varchar(2) NOT NULL,
    nome nvarchar(50) NOT NULL,
    id_carrinho BIGINT,
    id_historico_compras BIGINT,
    id_historico_visualizacoes BIGINT,
    FOREIGN KEY(id_carrinho) REFERENCES tbl_carrinho(id),
    FOREIGN KEY(id_historico_compras) REFERENCES tbl_historico_compras(id),
    FOREIGN KEY(id_historico_visualizacoes) REFERENCES tbl_historico_visualizacoes(id)
);

CREATE TABLE tbl_categoria(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    popularidade tinyint CHECK(popularidade BETWEEN 0 AND 100) NOT NULL,
    nome nvarchar(50) NOT NULL
)


--TABELAS ASSOCIATIVAS

CREATE TABLE tbl_historico_compras_produto(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    id_historico_compras BIGINT,
    id_produto BIGINT,
    FOREIGN KEY (id_produto) REFERENCES tbl_produto(id),
    FOREIGN KEY (id_historico_compras) REFERENCES tbl_historico_compras(id)
);

CREATE TABLE tbl_carrinho_produto(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    id_carrinho BIGINT,
    id_produto BIGINT,
    FOREIGN KEY (id_produto) REFERENCES tbl_produto(id),
    FOREIGN KEY (id_carrinho) REFERENCES tbl_carrinho(id)
);

CREATE TABLE tbl_categoria_produto(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    id_categoria BIGINT,
    id_produto BIGINT,
    FOREIGN KEY (id_produto) REFERENCES tbl_produto(id),
    FOREIGN KEY (id_categoria) REFERENCES tbl_categoria(id)
);

CREATE TABLE tbl_historico_visualizacoes_produto(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    id_historico_visualizacoes BIGINT,
    id_produto BIGINT,
    FOREIGN KEY (id_produto) REFERENCES tbl_produto(id),
    FOREIGN KEY (id_historico_visualizacoes) REFERENCES tbl_historico_visualizacoes(id)
);




--TRIGGERS 

CREATE TRIGGER incrementar_acessos
ON tbl_historico_visualizacoes_produto
AFTER INSERT
AS
BEGIN
    UPDATE tbl_produto
    SET acessos = acessos + 1 
    FROM tbl_produto p 
    INNER JOIN inserted i ON p.id = i.id_produto;
END;


CREATE TRIGGER adicionar_compras
ON tbl_historico_compras_produto
AFTER INSERT
AS
BEGIN 
    UPDATE tbl_produto 
    SET compras = compras + 1 
    FROM tbl_produto p 
    INNER JOIN inserted i ON p.id = i.id_produto;
END;


CREATE TRIGGER verificar_novidade
ON tbl_produto
AFTER INSERT
AS 
BEGIN 
    UPDATE tbl_produto
    SET isLancamento = 0 
    WHERE DATEDIFF(DAY, dt_lancamento, GETDATE()) > 7 AND id = (SELECT id FROM inserted);
END;