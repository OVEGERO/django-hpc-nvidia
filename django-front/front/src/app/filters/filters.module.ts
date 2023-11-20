import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // <-- NgModel lives here

import { FiltersRoutingModule } from './filters-routing.module';
import { LayoutPageComponent } from './pages/layout-page/layout-page.component';
import { MainPageComponent } from './pages/main-page/main-page.component';
import { PrimengModule } from '../primeng/primeng.module';
import { UploadFileComponent } from './components/uploadFile/uploadFile.component';
import { CardImageConvComponent } from './components/cardImageConv/cardImageConv.component';
import { CardImageOriginalComponent } from './components/cardImageOriginal/cardImageOriginal.component';


@NgModule({
  declarations: [
    LayoutPageComponent,
    MainPageComponent,
    UploadFileComponent,
    CardImageConvComponent,
    CardImageOriginalComponent,
  ],
  imports: [
    CommonModule,
    FiltersRoutingModule,
    PrimengModule,
    FormsModule // <-- import the FormsModule before binding with [(ngModel)]
  ]
})
export class FiltersModule { }
