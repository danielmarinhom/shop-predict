package br.com.projects.cartpredict.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Table(name="tbl_produto")
@Getter
@Setter
public class Produto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id", columnDefinition = "BIGINT")
    Long id;

    @Column(name="nome", nullable = false, length = 50)
    String nome;

    @Column(name="popularidade", columnDefinition = "tinyint", nullable = false)
    Integer popularidade;

    @Column(name="dt_lancamento", columnDefinition = "datetime", nullable = false)
    LocalDateTime dtLancamento;

    @Column(name="acessos")
    Integer acessos;

    @Column(name="compras")
    Integer compras;

    @Column(name="preco", nullable = false)
    Double preco;

    @Column(name = "isOferta", columnDefinition = "bit")
    Boolean isOferta;

    @Column(name = "isLancamento", columnDefinition = "bit")
    Boolean isLancamento;
}
