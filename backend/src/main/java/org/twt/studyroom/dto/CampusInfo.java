package org.twt.studyroom.dto;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.twt.studyroom.model.Campus;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class CampusInfo {
    private Long id;
    private String name;

    public static CampusInfo fromEntity(Campus e) {
        return new CampusInfo(e.getId(), e.getName());
    }
}
