package org.twt.studyroom.handler;

import jakarta.validation.ConstraintViolationException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.twt.studyroom.dto.Result;

@RestControllerAdvice
public class BaseHandler {

    @ExceptionHandler(ConstraintViolationException.class)
    public Result validationError(ConstraintViolationException e) {
        return Result.invalid(e.getMessage());
    }
}
