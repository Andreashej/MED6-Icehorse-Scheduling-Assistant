import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UnassignedTestsComponent } from './unassigned-tests.component';

describe('UnassignedTestsComponent', () => {
  let component: UnassignedTestsComponent;
  let fixture: ComponentFixture<UnassignedTestsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UnassignedTestsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UnassignedTestsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
