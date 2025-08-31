$(document).ready(function(){
    $(".cancelBtn").on('click',function(){
        location.href='/cscenter/list/';
    });//cancelBtn

    $(".confirmBtn").on('click',function(){
        const form = $('#inquiryForm')[0];
        const formData = new FormData(form);

        // 유효성 검사
        if (formData.get('category_inq') === 'none') {
            alert('문의 유형을 선택해주세요.');
            return;
        }
        if (!formData.get('title_inq')?.trim()) {
            alert('제목을 입력해주세요.');
            return;
        }
        if (!formData.get('content_inq')?.trim()) {
            alert('내용을 입력해주세요.');
            return;
        }

        $.ajax({
            url:form.action,
            method:'POST',
            data:formData,
            processData:false,
            contentType:false,
            headers: {
                'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
            },
            success:function(data){
                if (data.success) {
                    alert('문의가 성공적으로 접수되었습니다.');
                    location.href='/cscenter/list/';
                } else {
                    alert('문의 접수 중 오류가 발생했습니다.');
                }
            },
            error: function(){
                alert('서버 오류가 발생했습니다.');
            }
        });//ajax
    });//confirmBtn
});//jquery ready