package org.twt.studyroom.controller;

import jakarta.annotation.Resource;
import org.hibernate.validator.constraints.Range;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.twt.studyroom.dto.Result;
import org.twt.studyroom.service.StudyRoomStatusService;

import java.time.LocalDate;

@RestController
@Validated
public class BaseController {


    @Resource
    private StudyRoomStatusService studyRoomStatusService;

    @GetMapping("/campus")
    public Result getCampusList() {
        return Result.success(
                studyRoomStatusService.getCampusList()
        );
    }

    @GetMapping("/campus/{campusId}/building")
    public Result getBuildingList(@PathVariable Long campusId) {
        return Result.success(
                studyRoomStatusService.getBuildingList(campusId)
        );
    }

    @GetMapping("/building/{buildingId}/room")
    public Result getRoomList(@PathVariable Long buildingId) {
        return Result.success(
                studyRoomStatusService.getRoomList(buildingId)
        );
    }

    @GetMapping("/building/{buildingId}/room/session/{sessionId}/date/{date}")
    public Result getBySession(
            @PathVariable Long buildingId,
            @PathVariable
            @Range(min = 1, max = 12, message = "sessionId must be between 1 and 12") int sessionId,
            @DateTimeFormat(pattern = "yyyy-MM-dd")
            @PathVariable LocalDate date) {
        return Result.success(
                studyRoomStatusService.getBySession(buildingId, sessionId, date)
        );
    }

    @GetMapping("/building/{buildingId}/free")
    public Result getRoomFree(@PathVariable Long buildingId) {
        return Result.success(
                studyRoomStatusService.getFreeRoom(buildingId)
        );
    }

    @GetMapping("/room/{roomId}/schedule")
    public Result getRoomSchedule(@PathVariable Long roomId) {
        return Result.success(
                studyRoomStatusService.getOccupy(roomId)
        );
    }
}
