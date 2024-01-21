package org.twt.studyroom.model.repo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.twt.studyroom.model.Building;

import java.util.List;

public interface BuildingRepo extends JpaRepository<Building, Long> {

    @Query("select a from Building a where a.campusId=?1 order by a.name asc")
    List<Building> getBuildings(Long campusId);
}
