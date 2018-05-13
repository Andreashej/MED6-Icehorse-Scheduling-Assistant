import { Component, OnInit} from '@angular/core';
import { AppComponent } from '../app.component';
import { SettingsProviderService } from '../settings-provider.service';
import { CompetitionImporterService } from '../competition-importer.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  name = '';
  settings = {
    'name': '',
    'tracks': []
  };
  currentlink = '/';
  activeTrack = '';

  constructor(private app: AppComponent,
    private settingsProvider: SettingsProviderService,
    private competitionImporter: CompetitionImporterService) { }

  ngOnInit() {
    this.getSettings();
  }

  setTitle(): void {
    this.name = this.settings.name;
    this.activeTrack = this.settings.tracks[0];
    this.competitionImporter.changeActiveTrack(this.activeTrack);
  }

  getSettings(): void {
    this.settingsProvider.getSettings().subscribe(
      data => this.settings = data[0],
      error => console.log('Error when fetching data'),
      () => this.setTitle()
    );
  }

  changeTrack(): void {
    this.competitionImporter.changeActiveTrack(this.activeTrack);
  }

}
