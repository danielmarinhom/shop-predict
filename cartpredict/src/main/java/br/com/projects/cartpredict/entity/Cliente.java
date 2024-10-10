package br.com.projects.cartpredict.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Entity
@Table(name="tbl_cliente")
@Getter
@Setter
public class Cliente {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id", columnDefinition = "BIGINT")
    Long id;

    @Column(name="dt_nasc", nullable = false)
    Date dtNasc;

    @Column(name="genero", length = 1, nullable = false)
    char genero;

    @Column(name="cidade", nullable = false)
    String cidade;

    @Column(name="estado", length = 2, nullable = false)
    String estado;

    @Column(name="nome", nullable = false, length = 50)
    String nome;

    @OneToOne
    @JoinColumn(id_carrinho)
    private Carrinho carrinho;

    @OneToOne
    @JoinColumn(id_historico_compras)
    private HistoricoCompras historicoCompras;

    @OneToOne
    @JoinColumn(id_historico_visualizacoes)
    private HistoricoVisualizacoes historicoVisualizacoes;


}
