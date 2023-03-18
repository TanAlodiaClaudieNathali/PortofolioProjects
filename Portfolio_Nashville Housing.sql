--Cleaning Data in SQL

Select *
From Portofolio.dbo.[Nashville Housing]

--Standardize Date Format using CONVERT
Select SaleDateConverted, CONVERT(Date,SaleDate)
From Portofolio.dbo.[Nashville Housing]

Update [Nashville Housing]
set SaleDate = Convert(Date,SaleDate)

Alter Table [Nashville Housing]
Add SaleDateConverted Date;

--------------------------------------------------------------------------------------
--Populate Property Address Data by breaking the data

Select *
From Portofolio.dbo.[Nashville Housing]
--where PropertyAddress is null
order by ParcelID

Select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, isnull(a.PropertyAddress, b.PropertyAddress)
From Portofolio.dbo.[Nashville Housing] a
Join Portofolio.dbo.[Nashville Housing] b
	on a.ParcelID = b.ParcelID
	and a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is null

UPDATE a
SET PropertyAddress = isnull(a.PropertyAddress, b.PropertyAddress)
From Portofolio.dbo.[Nashville Housing] a
Join Portofolio.dbo.[Nashville Housing] b
	on a.ParcelID = b.ParcelID
	and a.[UniqueID ] <> b.[UniqueID ]

--null property address is updated with corresponding values

--------------------------------------------------------------------------------------
--Breaking out Address into Individual Columns (Address, City, State) by using SUBSTRING
Select PropertyAddress
from Portofolio.dbo.[Nashville Housing]

--comma is the delimiter, choose the specific data
select
substring(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1) as Address,
substring(PropertyAddress, CHARINDEX(',', PropertyAddress)+1, len(PropertyAddress)) as Address
from Portofolio.dbo.[Nashville Housing]

--make new columns and update
Alter Table [Nashville Housing]
Add PropertySplitAddress Nvarchar(255);

Update [Nashville Housing]
set PropertySplitAddress = substring(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1)

--make new column and update
Alter Table [Nashville Housing]
Add PropertySplitCity nvarchar(255);

Update [Nashville Housing]
set PropertySplitCity = substring(PropertyAddress, CHARINDEX(',', PropertyAddress)+1, len(PropertyAddress))


--splitting owner address by using PARSENAME
Select OwnerAddress
from Portofolio.dbo.[Nashville Housing]

select
parsename(replace(ownerAddress, ',', '.'), 1),
parsename(replace(ownerAddress, ',', '.'), 2),
parsename(replace(ownerAddress, ',', '.'), 3)
from Portofolio.dbo.[Nashville Housing]

--make new columns for owner address
Alter Table Portofolio.dbo.[Nashville Housing]
Add OwnerSplitState Nvarchar(255);

Update Portofolio.dbo.[Nashville Housing]
set OwnerSplitState = parsename(replace(ownerAddress, ',', '.'), 1)

Alter Table Portofolio.dbo.[Nashville Housing]
Add OwnerSplitCity Nvarchar(255);

Update Portofolio.dbo.[Nashville Housing]
set OwnerSplitCity = parsename(replace(ownerAddress, ',', '.'), 2)


Alter Table Portofolio.dbo.[Nashville Housing]
Add OwnerSplitAddress Nvarchar(255);

Update Portofolio.dbo.[Nashville Housing]
set OwnerSplitAddress = parsename(replace(ownerAddress, ',', '.'), 3)

--check created columns
Select OwnerSplitAddress, OwnerSplitCity, OwnerSplitState
from Portofolio.dbo.[Nashville Housing]

-------------------------------------------------------------------------------
--change Y and N to Yes and No in "Sold as Vacant" field by using CASE

select Distinct(SoldAsVacant), count(SoldAsVacant)
from Portofolio.dbo.[Nashville Housing]
group by SoldAsVacant
order by 2

select SoldAsVacant,
case when SoldAsVacant = 'Y' then 'Yes'
	 when SoldAsVacant = 'N' then 'No'
	 else SoldAsVacant
	 end
from Portofolio.dbo.[Nashville Housing]

update Portofolio.dbo.[Nashville Housing]
set SoldAsVacant = case when SoldAsVacant = 'Y' then 'Yes'
	 when SoldAsVacant = 'N' then 'No'
	 else SoldAsVacant
	 end

-------------------------------------------------------------------------------
--remove duplicates by using CTE
with RowNumCTE as(
select *, 
	ROW_NUMBER() over(
	Partition by ParcelID,
				 PropertyAddress,
				 SalePrice,
				 SaleDate,
				 LegalReference
				 order by
					uniqueID) row_num

from Portofolio.dbo.[Nashville Housing]
--order by ParcelID
)

delete
from RowNumCTE
where row_num > 1
--order by PropertyAddress

---------------------------------------------------------------------------------------
--delete unused columns (OwnerAddress, PropertyAddress by DROP COLUMN
alter table Portofolio.dbo.[Nashville Housing]
drop column OwnerAddress, TaxDistrict, PropertyAddress

alter table Portofolio.dbo.[Nashville Housing]
drop column SaleDate

--final check

select *
from Portofolio.dbo.[Nashville Housing]
