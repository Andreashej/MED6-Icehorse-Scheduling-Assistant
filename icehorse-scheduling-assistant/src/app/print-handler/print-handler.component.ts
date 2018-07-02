import { Component, OnInit } from '@angular/core';
import { AppComponent } from '../app.component';
import { SettingsProviderService } from '../settings-provider.service';
import { FormsModule } from '@angular/forms';
import { CompetitionImporterService } from '../competition-importer.service';

@Component({
  selector: 'app-print-handler',
  templateUrl: './print-handler.component.html',
  styleUrls: ['./print-handler.component.css']
})
export class PrintHandlerComponent implements OnInit {
  name = '';
  settings;
  template = '';
  judges;

  constructor(private app: AppComponent,
    private settingsProvider: SettingsProviderService,
    private competitionImporter: CompetitionImporterService) { }

  ngOnInit() {
    this.getSettings();
    this.getJudges();
  }

  getJudges() {
    this.competitionImporter.getAllJudges().subscribe(
      judgelist => this.judges = judgelist,
      () => console.log('Could not retrieve judges')
    );
  }

  getSettings(): void {
    this.settingsProvider.getSettings().subscribe(
      data => this.settings = data,
      error => console.log('Error when fetching data'),
      () => console.log('Got settings')
    );
  }

  toDate(day): Date {
    return new Date(day);
  }

  print(): void {
    setTimeout(100);
    window.print();
  }

}
