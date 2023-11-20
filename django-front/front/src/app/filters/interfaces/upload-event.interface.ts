import { HttpEvent } from "@angular/common/http";

export interface UploadEvent {
  originalEvent: HttpEvent<any>;
  files: File[];
}
