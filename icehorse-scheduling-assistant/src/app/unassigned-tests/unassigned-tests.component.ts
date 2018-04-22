import { Component, OnInit } from '@angular/core';
import { CompetitionImporterService } from '../competition-importer.service';
import { NgDragDropModule } from 'ng-drag-drop';

@Component({
  selector: 'app-unassigned-tests',
  templateUrl: './unassigned-tests.component.html',
  styleUrls: ['./unassigned-tests.component.css']
})
export class UnassignedTestsComponent implements OnInit {
  testdata;
  droppedItems = [];
  loading = false;

  constructor(private competitionImporter: CompetitionImporterService) { }

  ngOnInit() {
  }

  getTestData(): void {
    this.competitionImporter.getTestData().subscribe(
        data => this.testdata = data
    );
  }

  reloadTestData(): void {
    this.loading = true;
    this.competitionImporter.refreshTestData().subscribe(
      data => this.testdata = data,
      () => console.log('Error when reloading'),
      () => this.loading = false
    );
  }

  onDrop(e: any) {
    console.log(e.dragData);
    this.droppedItems.push(e.dragData);
  }

  removeUnassigned(e: any) {
    console.log(e);
    this.testdata.splice(this.testdata.indexOf(e), 1);
  }

}
