package org.twt.studyroom.model.repo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.twt.studyroom.model.Room;
import org.twt.studyroom.model.Status;

import java.time.LocalDate;
import java.util.Set;

public interface StatusRepo extends JpaRepository<Status, Long> {


    @Query("SELECT r FROM Room r WHERE r.buildingId = ?1 AND EXISTS (SELECT d FROM Status d WHERE d.roomId = r.id AND d.sessionIndex = ?2 AND d.date=?3) ORDER BY r.name ASC")
    Set<Room> getFreeRoom(Long buildingId, Integer sessionIndex, LocalDate date);

    @Query("SELECT status FROM Status status WHERE status.roomId=?1")
    Set<Status> getOccupy(Long roomId);

}
