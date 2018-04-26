import { Component, OnInit } from '@angular/core';
import { AppComponent } from '../app.component';
import { SettingsProviderService } from '../settings-provider.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  name = '';
  settings;

  constructor(private app: AppComponent, private settingsProvider: SettingsProviderService) { }

  ngOnInit() {
    this.getSettings();
    this.name = this.app.title;
  }

  setTitle(): void {
    this.name += ' | ' + this.settings[0].name;
  }

  getSettings(): void {
    this.settingsProvider.getSettings().subscribe(
      data => this.settings = data,
      error => console.log('Error when fetching data'),
      () => this.setTitle()
    );
  }

}
