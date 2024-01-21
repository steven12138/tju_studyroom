package org.twt.studyroom.model;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "campus")
@Getter
@Setter
@ToString
@AllArgsConstructor
@NoArgsConstructor
public class Campus {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(name = "name", nullable = false,unique = true)
    private String name;
}
