import {JupyterFrontEnd, JupyterFrontEndPlugin} from '@jupyterlab/application';

import {ICommandPalette} from '@jupyterlab/apputils';

import {PageConfig} from '@jupyterlab/coreutils';

import {ILauncher} from '@jupyterlab/launcher';

import '../style/index.css';

const LAUNCH_COMMAND = 'omnisci:launch-immerse';

/**
 * Initialization data for the jupyterlab-immerse extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-immerse',
  autoStart: true,
  requires: [ICommandPalette, ILauncher],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    launcher: ILauncher,
  ) => {
    app.commands.addCommand(LAUNCH_COMMAND, {
      label: args => args['isLauncher'] ? 'OmniSci Immerse' : 'Launch OmniSci Immerse',
      caption: 'Launch OmniSci Immerse',
      iconClass: 'immerse-OmniSciLogo',
      execute: () => window.open(`${PageConfig.getBaseUrl()}immerse`, '_blank')
    });
    launcher.add({
      category: 'Other',
      rank: 10,
      args: { isLauncher: true },
      command: LAUNCH_COMMAND
    });
    palette.addItem({
      category: 'OmniSci',
      command: LAUNCH_COMMAND
    });
  },
};

export default extension;
