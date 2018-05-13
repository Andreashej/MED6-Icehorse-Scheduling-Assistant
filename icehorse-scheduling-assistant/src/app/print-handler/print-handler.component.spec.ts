import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PrintHandlerComponent } from './print-handler.component';

describe('PrintHandlerComponent', () => {
  let component: PrintHandlerComponent;
  let fixture: ComponentFixture<PrintHandlerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PrintHandlerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PrintHandlerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
