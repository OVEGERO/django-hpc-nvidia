import { NgModule } from '@angular/core';

import { DropdownModule } from 'primeng/dropdown';
import { InputNumberModule } from 'primeng/inputnumber';
import { FileUploadModule } from 'primeng/fileupload';
import { ImageModule } from 'primeng/image';
import { CardModule } from 'primeng/card';
import { TooltipModule } from 'primeng/tooltip';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';
import { AccordionModule } from 'primeng/accordion';

@NgModule({
  declarations: [],
  exports: [
    DropdownModule,
    InputNumberModule,
    FileUploadModule,
    ImageModule,
    CardModule,
    TooltipModule,
    ButtonModule,
    ToastModule,
    AccordionModule,
  ]
})
export class PrimengModule { }
