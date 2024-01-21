package org.twt.studyroom.model;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;
import java.util.Objects;

@Entity
@Table(name = "status")
@Getter
@Setter
@ToString
@AllArgsConstructor
@NoArgsConstructor
public class Status {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(name = "room_id", nullable = false)
    private Long roomId;

    @Column(name = "date", nullable = false)
    private LocalDate date;

    @Column(name = "session_index", nullable = false)
    private Integer sessionIndex;

    @Override
    public boolean equals(Object other) {
        if (this == other) return true;
        if (other == null || getClass() != other.getClass()) return false;
        Status status = (Status) other;

        // 如果id为null，则只比较date和session_index
        if (id == null) {
            return Objects.equals(sessionIndex, status.sessionIndex) && Objects.equals(date, status.date);
        } else {
            return Objects.equals(id, status.id);
        }
    }

    @Override
    public int hashCode() {
        return Objects.hash(date, sessionIndex);
    }
}