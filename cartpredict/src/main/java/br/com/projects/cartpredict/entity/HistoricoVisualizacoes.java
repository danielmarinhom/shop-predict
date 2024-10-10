package br.com.projects.cartpredict.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Table(name="tbl_historico_visualizacoes")
@Getter
@Setter
public class HistoricoVisualizacoes {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id", columnDefinition = "BIGINT")
    Long id;
}
