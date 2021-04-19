class ContextMixin:
    def get_user_context(self, **kwargs):
        """Метод для передачи в контекст класса представления собственных
        переменных (например, title), если это необходимо"""
        context = super().get_context_data()
        for key, value in kwargs.items():
            context[key] = value
        return context
