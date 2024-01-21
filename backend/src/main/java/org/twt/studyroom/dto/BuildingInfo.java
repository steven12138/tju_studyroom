package org.twt.studyroom.dto;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import io.netty.util.internal.StringUtil;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.twt.studyroom.model.Building;

@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
@AllArgsConstructor
@NoArgsConstructor
public class BuildingInfo {
    private long id;
    private String name;
    private Long campusId;

    public static BuildingInfo fromEntity(Building e) {
        return new BuildingInfo(
                e.getId(),
                !StringUtil.isNullOrEmpty(e.getMappedName()) ? e.getMappedName() : e.getName(),
                e.getCampusId()
        );
    }

}
