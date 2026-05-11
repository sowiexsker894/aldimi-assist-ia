export interface MenuNodeDto {
  id: number;
  path: string;
  label: string;
  icon: string | null;
  sort_order: number;
  children: MenuNodeDto[];
}

export interface UserSummaryDto {
  id: number;
  email: string;
  full_name: string;
  roles: string[];
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: UserSummaryDto;
  menu: MenuNodeDto[];
}

export interface MeResponse {
  user: UserSummaryDto;
  menu: MenuNodeDto[];
}
