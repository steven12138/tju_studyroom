package org.twt.studyroom.model.repo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.twt.studyroom.model.Room;

import java.util.List;

public interface RoomRepo extends JpaRepository<Room, Long> {

    @Query("select a from Room a where a.buildingId=?1 order by a.name asc")
    List<Room> getRoomList(Long buildingId);
}
