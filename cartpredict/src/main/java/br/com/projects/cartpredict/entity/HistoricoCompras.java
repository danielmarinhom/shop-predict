package br.com.projects.cartpredict.entity;


import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Entity
@Table(name="tbl_historico_compras")
@Getter
@Setter
public class HistoricoCompras {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id", columnDefinition = "BIGINT")
    Long id;

    @ManyToMany
            @JoinTable(name="tbl_produto", joinColumns = @JoinColumn(name = "id"), inverseJoinColumns = )
    List<Produto> produtos;
}
