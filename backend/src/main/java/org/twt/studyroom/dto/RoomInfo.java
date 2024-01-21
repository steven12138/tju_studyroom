package org.twt.studyroom.dto;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import io.netty.util.internal.StringUtil;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.twt.studyroom.model.Room;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class RoomInfo {
    private Long id;
    private String name;
    private String buildingId;
    private boolean isFree;

    public static RoomInfo fromEntity(Room e) {
        return new RoomInfo(
                e.getId(),
                !StringUtil.isNullOrEmpty(e.getMappedName()) ? e.getMappedName() : e.getName(),
                e.getBuildingId(),
                true
        );
    }

}
