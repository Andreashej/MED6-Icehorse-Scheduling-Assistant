import { Component, OnInit } from '@angular/core';
import { SettingsProviderService } from '../settings-provider.service';
import { CompetitionImporterService } from '../competition-importer.service';
import { GlobalUpdateService } from '../global-update.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {

  constructor(private settingsProvider: SettingsProviderService,
              private competitionImporter: CompetitionImporterService,
              private updateHandler: GlobalUpdateService) { }
  settings;
  tests;

  ngOnInit() {
    this.settingsProvider.getSettings().subscribe(
      data => this.settings = data
    );

    this.competitionImporter.getAllTestData().subscribe(
      data => this.tests = data
    );
  }

  saveTest(testId, testcode, timeperheat, lr, rr) {
    this.competitionImporter.saveTest(testId, testcode, lr, rr, timeperheat).subscribe(
      () => {
        this.competitionImporter.getAllTestData().subscribe(
          data => this.tests = data
        );
      }
    );
  }

  createTest(testcode, lr, rr, base) {
    this.competitionImporter.createTest(testcode, lr, rr, base).subscribe(
      () => {
        this.competitionImporter.getAllTestData().subscribe(
          data => this.tests = data
        );
      }
    );
  }

}
