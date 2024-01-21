package org.twt.studyroom.dto;

import lombok.Data;
import org.twt.studyroom.utils.ReturnCode;

/**
 * The type Result.
 */
@Data
public class Result {


    private int code;
    private Object data;

    /**
     * Instantiates a new Result.
     *
     * @param code the code
     * @param data the data
     */
    public Result(int code, Object data) {
        this.code = code;
        this.data = data;
    }

    /**
     * Success result.
     *
     * @param data the data
     * @return the result
     */
    public static Result success(Object data) {
        return new Result(ReturnCode.Success.getCode(), data);
    }

    /**
     * Success result.
     *
     * @return the result
     */
    public static Result success() {
        return new Result(ReturnCode.Success.getCode(), "success");
    }

    /**
     * Failure result.
     *
     * @param code the code
     * @return the result
     */
    public static Result failure(ReturnCode code) {
        return new Result(code.getCode(), code.getMessage());
    }

    public static Result invalid(String message) {
        return new Result(ReturnCode.InvalidParams.getCode(), message);
    }


}
