package org.twt.studyroom.service;

import org.twt.studyroom.dto.BuildingInfo;
import org.twt.studyroom.dto.CampusInfo;
import org.twt.studyroom.dto.OccupyInfo;
import org.twt.studyroom.dto.RoomInfo;

import java.time.LocalDate;
import java.util.List;

public interface StudyRoomStatusService {
    List<CampusInfo> getCampusList();

    List<BuildingInfo> getBuildingList(Long campusId);

    List<RoomInfo> getRoomList(Long buildingId);

    List<RoomInfo> getFreeRoom(Long buildingId);

    List<RoomInfo> getBySession(Long buildingId, int sessionId, LocalDate date);

    List<OccupyInfo> getOccupy(Long roomId);
}
