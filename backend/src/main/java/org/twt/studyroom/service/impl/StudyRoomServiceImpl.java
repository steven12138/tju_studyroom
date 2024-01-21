package org.twt.studyroom.service.impl;

import jakarta.annotation.Resource;
import org.springframework.stereotype.Service;
import org.twt.studyroom.dto.BuildingInfo;
import org.twt.studyroom.dto.CampusInfo;
import org.twt.studyroom.dto.OccupyInfo;
import org.twt.studyroom.dto.RoomInfo;
import org.twt.studyroom.model.Room;
import org.twt.studyroom.model.Status;
import org.twt.studyroom.model.repo.BuildingRepo;
import org.twt.studyroom.model.repo.CampusRepo;
import org.twt.studyroom.model.repo.RoomRepo;
import org.twt.studyroom.model.repo.StatusRepo;
import org.twt.studyroom.service.StudyRoomStatusService;
import org.twt.studyroom.utils.SessionIndexUtil;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Service
public class StudyRoomServiceImpl implements StudyRoomStatusService {

    @Resource
    private CampusRepo campusRepo;

    @Resource
    private BuildingRepo buildingRepo;

    @Override
    public List<CampusInfo> getCampusList() {
        return campusRepo.getCampus()
                .stream()
                .map(CampusInfo::fromEntity)
                .toList();
    }

    @Override
    public List<BuildingInfo> getBuildingList(Long campusId) {
        return buildingRepo.getBuildings(campusId)
                .stream()
                .map(BuildingInfo::fromEntity)
                .toList();
    }

    @Resource
    private RoomRepo roomRepo;


    @Override
    public List<RoomInfo> getRoomList(Long buildingId) {
        return getBySession(buildingId, SessionIndexUtil.getCurrentSessionIndex(), LocalDate.now());
    }

    @Resource
    private StatusRepo statusRepo;

    @Override
    public List<RoomInfo> getFreeRoom(Long buildingId) {
        int sessionIndex = SessionIndexUtil.getCurrentSessionIndex();
        if (sessionIndex == -1) {
            return roomRepo.getRoomList(buildingId)
                    .stream()
                    .map(RoomInfo::fromEntity)
                    .toList();
        }
        return statusRepo.getFreeRoom(buildingId, sessionIndex, LocalDate.now())
                .stream().map(RoomInfo::fromEntity)
                .toList();
    }

    @Override
    public List<RoomInfo> getBySession(Long buildingId, int sessionId, LocalDate date) {
        if (sessionId == -1) {
            return roomRepo.getRoomList(buildingId)
                    .stream()
                    .map(RoomInfo::fromEntity)
                    .toList();
        }
        Set<Room> freeRoom = new HashSet<>(statusRepo.getFreeRoom(buildingId, sessionId, date));
        return roomRepo.getRoomList(buildingId)
                .stream()
                .map(e -> {
                    RoomInfo roomInfo = RoomInfo.fromEntity(e);
                    roomInfo.setFree(freeRoom.contains(e));
                    return roomInfo;
                })
                .toList();
    }

    @Override
    public List<OccupyInfo> getOccupy(Long roomId) {
        Set<Status> freeStates = statusRepo.getOccupy(roomId);
        freeStates.forEach(System.out::println);
        List<OccupyInfo> occupyInfos = new ArrayList<>();
        LocalDate now = LocalDate.now();

        for (int day = 0; day < 7; day++) {
            LocalDate date = now.plusDays(day);
            for (int sessionIndex = 1; sessionIndex <= 12; sessionIndex++) {
                Status statusToCheck = new Status(null, roomId, date, sessionIndex);
                // 如果 freeStates 不包含这个状态，则认为这个时段被占用
                if (!freeStates.contains(statusToCheck)) {
                    occupyInfos.add(new OccupyInfo(date, sessionIndex));
                }
            }
        }
        return occupyInfos;
    }

}
