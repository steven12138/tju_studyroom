package org.twt.studyroom.model.repo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.twt.studyroom.model.Campus;

import java.util.List;

public interface CampusRepo extends JpaRepository<Campus, Integer> {
    @Query("select a from Campus a order by a.name asc")
    List<Campus> getCampus();
}
