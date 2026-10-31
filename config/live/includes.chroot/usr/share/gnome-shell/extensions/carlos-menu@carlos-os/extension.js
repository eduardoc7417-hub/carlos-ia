import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import GObject from 'gi://GObject';
import St from 'gi://St';

import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';
import * as Util from 'resource:///org/gnome/shell/misc/util.js';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';

const ITEMS = [
    ['Sobre este computador', ['gnome-control-center', 'system', 'about']],
    ['Configurações', ['gnome-control-center']],
    ['Papel de parede', ['gnome-control-center', 'background']],
    null,
    ['Bloquear a tela', ['loginctl', 'lock-session']],
    ['Encerrar a sessão', ['gnome-session-quit', '--logout']],
    null,
    ['Suspender', ['systemctl', 'suspend']],
    ['Reiniciar', ['gnome-session-quit', '--reboot']],
    ['Desligar', ['gnome-session-quit', '--power-off']],
];

const AuroraButton = GObject.registerClass(
class AuroraButton extends PanelMenu.Button {
    _init() {
        super._init(0.0, 'Menu Aurora');
        this.add_child(new St.Icon({
            gicon: Gio.icon_new_for_string('/usr/share/pixmaps/carlos-logo.png'),
            icon_size: 18,
        }));
        for (const item of ITEMS) {
            if (item)
                this.menu.addAction(item[0], () => Util.spawn(item[1]));
            else
                this.menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());
        }
    }
});

export default class CarlosMenu extends Extension {
    enable() {
        this._button = new AuroraButton();
        Main.panel.addToStatusArea(this.uuid, this._button, 0, 'left');
        // O GNOME abre na visão geral: o Carlos OS abre direto na área de trabalho.
        this._hideId = GLib.timeout_add(GLib.PRIORITY_DEFAULT, 1500, () => {
            Main.overview.hide();
            this._hideId = 0;
            return GLib.SOURCE_REMOVE;
        });
    }

    disable() {
        if (this._hideId)
            GLib.source_remove(this._hideId);
        this._hideId = 0;
        this._button.destroy();
        this._button = null;
    }
}
