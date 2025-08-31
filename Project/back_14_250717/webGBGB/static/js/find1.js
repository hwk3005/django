$(document).ready(function() {
    let isEmailSent = false;
    let isVerified = false;
    
    // 이메일 전송 버튼 클릭
    $('#sendEmailBtn').click(function(e) {
        e.preventDefault();
        
        const name = $('#nameInput').val().trim();
        const email = $('#emailInput').val().trim();

        if (!name) {
            alert('이름을 입력해주세요.');
            return;
        }

        if (!email) {
            alert('이메일을 입력해주세요.');
            return;
        }
        
        // 이메일 형식 간단 체크
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert('올바른 이메일 형식을 입력해주세요.');
            return;
        }
        
        // 버튼 비활성화
        $(this).prop('disabled', true).text('전송중...');
        
        $.ajax({
            url: '/member/send-verification/',
            type: 'POST',
            data: {
                'name': name,
                'email': email,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                    isEmailSent = true;
                    $('#sendEmailBtn').text('재전송').prop('disabled', false);
                } else {
                    alert(response.message);
                    $('#sendEmailBtn').text('전송').prop('disabled', false);
                }
            },
            error: function() {
                alert('서버 오류가 발생했습니다.');
                $('#sendEmailBtn').text('전송').prop('disabled', false);
            }
        });
    });
    
    // 인증번호 확인 버튼 클릭
    $('#verifyBtn').click(function(e) {
        e.preventDefault();
        
        const verificationCode = $('#verificationInput').val().trim();
        if (!verificationCode) {
            alert('인증번호를 입력해주세요.');
            return;
        }
        
        // 버튼 비활성화
        $(this).prop('disabled', true).text('인증중...');
        
        $.ajax({
            url: '/member/verify-code/',
            type: 'POST',
            data: {
                'verification_code': verificationCode,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                    isVerified = true;
                    $('#verifyBtn').text('인증완료').prop('disabled', true);
                    $('#foundIdSection').show();
                    $('#foundId').text(response.user_id);
                } else {
                    alert(response.message);
                    $('#verifyBtn').text('인증').prop('disabled', false);
                }
            },
            error: function() {
                alert('서버 오류가 발생했습니다.');
                $('#verifyBtn').text('인증').prop('disabled', false);
            }
        });
    });
});