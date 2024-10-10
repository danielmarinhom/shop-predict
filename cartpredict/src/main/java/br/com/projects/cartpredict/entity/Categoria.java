package br.com.projects.cartpredict.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Table(name="tbl_categoria")
@Getter
@Setter
public class Categoria {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id", columnDefinition = "BIGINT")
    Long id;

    @Column(name="nome", nullable = false, length = 50)
    String nome;

    @Column(name="popularidade", columnDefinition = "tinyint", nullable = false)
    Integer popularidade;


}
