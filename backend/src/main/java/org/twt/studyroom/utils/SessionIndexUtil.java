package org.twt.studyroom.utils;

import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

public class SessionIndexUtil {
    static class ClassPeriod {
        LocalTime startTime;
        LocalTime endTime;

        public ClassPeriod(LocalTime startTime, LocalTime endTime) {
            this.startTime = startTime;
            this.endTime = endTime;
        }

        boolean isInPeriod(LocalDateTime time) {
            LocalTime t = time.toLocalTime();
            return !t.isBefore(startTime) && t.isBefore(endTime);
        }

        boolean isInPeriod(LocalTime t) {
            return !t.isBefore(startTime) && t.isBefore(endTime);
        }
    }

    private static final List<ClassPeriod> periods = new ArrayList<>();

    static {

        periods.add(new ClassPeriod(LocalTime.of(8, 30), LocalTime.of(9, 15)));
        periods.add(new ClassPeriod(LocalTime.of(9, 20), LocalTime.of(10, 5)));

        periods.add(new ClassPeriod(LocalTime.of(10, 25), LocalTime.of(11, 10)));
        periods.add(new ClassPeriod(LocalTime.of(11, 15), LocalTime.of(12, 0)));
        /*
            --- 午休 ---
        */
        periods.add(new ClassPeriod(LocalTime.of(13, 30), LocalTime.of(14, 15)));
        periods.add(new ClassPeriod(LocalTime.of(14, 20), LocalTime.of(15, 5)));

        periods.add(new ClassPeriod(LocalTime.of(15, 25), LocalTime.of(16, 10)));
        periods.add(new ClassPeriod(LocalTime.of(16, 15), LocalTime.of(17, 0)));
        /*
            --- 晚餐 ---
        */
        periods.add(new ClassPeriod(LocalTime.of(18, 30), LocalTime.of(19, 15)));
        periods.add(new ClassPeriod(LocalTime.of(19, 20), LocalTime.of(20, 5)));
        periods.add(new ClassPeriod(LocalTime.of(20, 10), LocalTime.of(20, 55)));
        periods.add(new ClassPeriod(LocalTime.of(21, 0), LocalTime.of(21, 45)));
    }

    public static int getCurrentSessionIndex() {
        LocalTime currentTime = LocalTime.now();
        for (int i = 0; i < periods.size(); i++) {
            ClassPeriod period = periods.get(i);
            if (period.isInPeriod(currentTime)) {
                return i + 1;
            }
        }
        return -1;
    }
}
