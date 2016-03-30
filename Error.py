import SimpleHTTPServer

INVALID_USER_ERROR = 'Not Exist User'
NOT_FOUND_ERROR = 'Page Not Found'
PASSWORD_NOT_MATCH_ERROR = 'Password Not Match'
PERMISSION_NOT_ALLOW_ERROR = 'Permission Not Allow'
UNKNOWN_ERROR = 'Unknown Error'


HTTPERROR_SESSION_IS_NOT_MATCH = 993    # �ٸ� Ŭ���̾�Ʈ���� �α��� �ؼ� ���Ǿ��̵� �ٲ� ���
HTTPERROR_SESSION_EXPIRED = 996         # ���� ���̵� memcache ���� ���ư� ���
HTTPERROR_NO_SESSIONID_IN_COOKIE = 994  # Ŭ���̾�Ʈ�� ��Ű�� ���� sid �� ��� �ϴµ� ���� ������.
HTTPERROR_LOGINTIME_OVER = 995          # Ŭ�󿡼� �� ��Ŷ�� ������ ��Ŷ (���� ��Ŷ�� ���� ��Ŷ�� �ð�����)
HTTPERROR_MISMATCH_ENCRYPT_ERROR = 990  # Ŭ���̾�Ʈ�� ������ Ű�� ���� ����
HTTPERROR_PACKET_NO_ENCRYPT_ERROR = 991  # ���ǿ� ��ȣŰ�� ����
HTTPERROR_PACKET_NOT_ENCRYPT_ERROR = 992  # ��Ŷ ����� Ű�� ����
HTTPERROR_CONTENTS_OFF = 600  # �ش� �������� ��� �Ǿ� ����
HTTPERROR_OUT_PERMISSION_ERROR = 997  # �ܺ� ���� �Ұ����� ����

class NotFoundError(object):
    code = NOT_FOUND_ERROR
    description = '<p>Page Not found</p>'


class PasswordNotMatchError(object):
    code = PASSWORD_NOT_MATCH_ERROR
    description = '<p>Password not matched</p>'


class PermissionNotAllowError(object):
    code = PERMISSION_NOT_ALLOW_ERROR
    description = '<p>Permission Not allow</p>'


class UnknownError(object):
    code = UNKNOWN_ERROR
    description = '<p>Unknown Error!</p>'

class E_DB_ERROR(object):
    EXCESS_ERROR = -1001 
    UNKNOWN_ERROR = -1002;

class ErrorView(object):
    def __init__(self, app):
        abort.mappings[NOT_FOUND_ERROR] = NotFoundError
        abort.mappings[PASSWORD_NOT_MATCH_ERROR] = PasswordNotMatchError
        abort.mappings[PERMISSION_NOT_ALLOW_ERROR] = PermissionNotAllowError
        abort.mappings[UNKNOWN_ERROR] = PermissionNotAllowError

        @app.errorhandler(NOT_FOUND_ERROR)
        def page_not_found(error):
            return render_template('page_not_found.html'), NOT_FOUND_ERROR

        @app.errorhandler(PASSWORD_NOT_MATCH_ERROR)
        def password_not_match(error):
            return render_template('password_not_match.html'), PASSWORD_NOT_MATCH_ERROR

        @app.errorhandler(PERMISSION_NOT_ALLOW_ERROR)
        def permission_not_allow(error):
            return render_template('permission_not_allow.html'), PERMISSION_NOT_ALLOW_ERROR

        @app.errorhandler(UNKNOWN_ERROR)
        def unknown_error(error):
            return render_template('unknown_error.html'), UNKNOWN_ERROR

