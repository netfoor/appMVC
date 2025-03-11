/* filepath: /home/netfoor/NextWork/clases-obj/flask-app/static/js/scripts.js */
document.addEventListener('alpine:init', () => {
    Alpine.data('lessonData', () => ({
        currentLesson: 1,
        draggedItems: [],
        codeInput: '',
        quizAnswers: {},
        activeTab: 'basics',
        showDefinition: false,
        showAnalogy: false,
        showAttributes: false,
        showMethods: false,
        showObjectExample: false,
        lesson: {
            title: 'Introducción a Clases y Objetos',
            description: 'Aprenderás los fundamentos de la Programación Orientada a Objetos.',
            interactive_elements: [
                {
                    type: 'drag-drop',
                    data: {
                        options: ['nombre', 'raza', 'edad', 'ladrar()', 'correr()']
                    }
                },
                {
                    type: 'code-editor'
                }
            ]
        }
    }));
});