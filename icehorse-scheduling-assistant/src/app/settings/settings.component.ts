import { Component, OnInit } from '@angular/core';
import { SettingsProviderService } from '../settings-provider.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {

  constructor(private settingsProvider: SettingsProviderService) { }
  settings;

  ngOnInit() {
    this.settingsProvider.getSettings().subscribe(
      data => this.settings = data
    );
  }

}
