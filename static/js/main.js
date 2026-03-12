// 前端交互增强
document.addEventListener('DOMContentLoaded', function () {
    // 为所有按钮和链接添加键盘支持提示
    const buttons = document.querySelectorAll('button, a');
    buttons.forEach(button => {
        button.addEventListener('keydown', function(e) {
            if(e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click(); // 模拟点击
            }
        });
    });

    // 表单提交前的简单验证（增强用户体验）
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // 可以在这里添加更复杂的验证逻辑
            console.log('Form submitted!');
        });
    });
});