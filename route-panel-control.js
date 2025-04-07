(function () {
  'use strict';

  function init () {
    /**
     * Создаем мультимаршрут.
     * Первым аргументом передаем модель либо объект описания модели.
     * Вторым аргументом передаем опции отображения мультимаршрута.
     * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/multiRouter.MultiRoute.xml
     * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/multiRouter.MultiRouteModel.xml
     */
    var multiRoute = new ymaps.multiRouter.MultiRoute({
        // Описание опорных точек мультимаршрута.
        referencePoints: [
            // [55.583556, 37.711356],
            // "Москва, МКАД, 25-й километр, вл4с1/6"
        ],
        // Параметры маршрутизации.
        params: {
            // Ограничение на максимальное количество маршрутов, возвращаемое маршрутизатором.
            results: 2
        }
    }, {
        // Автоматически устанавливать границы карты так, чтобы маршрут был виден целиком.
        boundsAutoApply: true
    });
    
    

    // Создаем кнопки для управления мультимаршрутом.
    var trafficButton = new ymaps.control.Button({
            data: { content: "Учитывать пробки" },
            options: { selectOnClick: true }
        });
        // viaPointButton = new ymaps.control.Button({
        //     data: { content: "Добавить транзитную точку" },
        //     options: { selectOnClick: true }
        // });

    // Объявляем обработчики для кнопок.
    trafficButton.events.add('select', function () {
        /**
         * Задаем параметры маршрутизации для модели мультимаршрута.
         * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/multiRouter.MultiRouteModel.xml#setParams
         */
        multiRoute.model.setParams({ avoidTrafficJams: true }, true);
    });

    trafficButton.events.add('deselect', function () {
        multiRoute.model.setParams({ avoidTrafficJams: false }, true);
    });

    // Создаем карту с добавленными на нее кнопками.
    var myMap = new ymaps.Map('map', {
        center: [55.583556, 37.711356],
        zoom: 12,
        controls: [
            trafficButton,
            'routePanelControl'
        ]
    }, {
        buttonMaxWidth: 300
    });

    // Добавляем мультимаршрут на карту.
    myMap.geoObjects.add(multiRoute);
    
    var control = myMap.controls.get('routePanelControl');

    control.options.set({
      autofocus: false
    });

    // Зададим состояние панели для построения машрутов.
    control.routePanel.state.set({
      // Тип маршрутизации.
      type: 'auto',
      // Выключим возможность задавать пункт отправления в поле ввода.
      toEnabled: false,
      // Адрес или координаты пункта отправления.
      to: 'Москва, МКАД, 25-й километр, вл4с1/6',
      // Включим возможность задавать пункт назначения в поле ввода.
      fromEnabled: true,
      // Адрес или координаты пункта назначения.
      //to: 'Петербург'
    });
      
    // Создадим элемент управления "Пробки".
    var trafficControl = new ymaps.control.TrafficControl({ state: {
            // Отображаются пробки "Сейчас".
            providerKey: 'traffic#actual',
            // Начинаем сразу показывать пробки на карте.
            trafficShown: false
        }});
    // Добавим контрол на карту.
    myMap.controls.add(trafficControl);
    // Получим ссылку на провайдер пробок "Сейчас" и включим показ инфоточек.
    trafficControl.getProvider('traffic#actual').state.set('infoLayerShown', true);
  }

  ymaps.ready(init);
  // window.mapsInit = init;

}());

//# sourceMappingURL=route-panel-control.js.map
