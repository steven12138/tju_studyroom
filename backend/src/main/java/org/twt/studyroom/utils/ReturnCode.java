package org.twt.studyroom.utils;

/**
 * The enum Return code.
 */
/*
code
1xxxx - success
2xxxx - failed
3xxxx - Privilege Problems
5xxxx - error
9xxxx - test
 */
public enum ReturnCode {
    /**
     * Success return code.
     */
//success
    Success(10000, "success"),

    /**
     * The Unknown failed.
     */
// failed
    UnknownFailed(20000, "Unknown Failed"),

    /**
     * The No privileges.
     */
// Privilege Error
    NoPrivileges(30000, "No Privilege"),
    /**
     * The User forbidden.
     */
    UserForbidden(30001, "You are blocked to login"),
    /**
     * The Captcha error.
     */
    CaptchaError(30002, "Captcha Error"),
    /**
     * The Username password not match.
     */
    UsernamePasswordNotMatch(30003, "username or password is not correct"),
    /**
     * The Password error.
     */
    PasswordError(30004, "Password Error"),
    /**
     * The Wrong security answer.
     */
    WrongSecurityAnswer(30005, "Security Answer Error"),
    /**
     * The Username exist.
     */
    UsernameExist(30006, "Username Exist"),
    /**
     * The User not activated.
     */
    UserNotActivated(30007, "User Not Activated"),
    /**
     * The Unknown department.
     */
    BlankValue(30008, "Blank Value"),
    /**
     * The Mail server connect failed.
     */
    MailSendFailed(30009, "mail send failed"),
    /**
     * The User not exist.
     */
    UserNotExist(30010, "User Not Exist"),
    InvalidEmail(30011, "Invalid Email"),
    RepeatEmail(30012, "Repeat Email"),

    /**
     * The Repeat value exception.
     */
    RepeatValueException(40000, "Repeat Value Exception"),
    DataNotFound(40001, "Request Data Not Exist"),
    PasswordRepeat(40002, "Password Repeat"),
    PublishRepeat(40003, "Publish Repeat"),

    /**
     * The Unknown error.
     */
// Error
    UnknownError(50000, "Server Unknown Error"),
    /**
     * The Invalid method.
     */
    InvalidMethod(50001, "Invalid Method"),
    /**
     * The Invalid params.
     */
    InvalidParams(50002, "Invalid Request Params"),
    /**
     * The Invalid value.
     */
    InvalidValue(50003, "Invalid Value"),

    /**
     * The Sql modification exception.
     */
    SQLModificationException(50004, "SQL Modification Exception"),
    /**
     * The Remote service error.
     */
    RemoteServiceError(50005, "Remote Service Get Error"),

    /**
     * The Time out error.
     */
    TimeOutError(50006, "Time Out Error"),
    /**
     * The Open ai service error.
     */
    OpenAIServiceError(50007, "OpenAI Service Error"),
    /**
     * The Save path not reachable.
     */
    SavePathNotReachable(50008, "Save Path Not Reachable"),
    /**
     * The Test api.
     */
//API TESTER
    testAPI(99999, "Test API");
    private final int code;
    private final String message;

    ReturnCode(int code, String message) {
        this.code = code;
        this.message = message;
    }

    /**
     * Gets code.
     *
     * @return the code
     */
    public int getCode() {
        return code;
    }

    /**
     * Gets message.
     *
     * @return the message
     */
    public String getMessage() {
        return message;
    }
}
