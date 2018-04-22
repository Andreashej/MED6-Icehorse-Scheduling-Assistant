import { Component, OnInit, Input } from '@angular/core';
import { NgDragDropModule } from 'ng-drag-drop';

@Component({
  selector: 'app-day',
  templateUrl: './day.component.html',
  styleUrls: ['./day.component.css']
})
export class DayComponent implements OnInit {
  @Input() date;
  droppedItems = [];

  onDropTest(test: any) {
    this.droppedItems.push(test.dragData);
  }

  constructor() { }

  ngOnInit() {
  }
}
